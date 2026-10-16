-- keep.lua: keep diagrams and short tables on one page.
--
-- Used by `make print` only. Before each diagram (a code block marked
-- `text`, or with no language) or table short enough to fit on a page,
-- it asks LaTeX (\needspace) for room for the whole of it, so that it
-- moves to the next page instead of being split. A diagram split
-- across two pages has to be pieced together by the reader; a program
-- listing reads line by line and may break, so listings in a language
-- are left alone. A heading directly above a kept block, with at most
-- one short paragraph between, moves with it. With KEEP_INTRO, a
-- paragraph that introduces a block, ending with a colon, is kept with
-- it too.

local MAX_CODE = 44   -- lines of code that fit on a page, with room left
local MAX_ROWS = 8    -- table rows likewise
local LINE_CHARS = 75 -- characters in a line of body text, roughly

local function code_lines(b)
  local n = 1
  for _ in b.text:gmatch('\n') do n = n + 1 end
  return n
end

local function table_rows(t)
  local n = #t.head.rows
  for _, body in ipairs(t.bodies) do n = n + #body.body end
  return n + #t.foot.rows
end

-- the space a block needs, in body lines, or nil to let it break
local function need(b)
  if b.t == 'CodeBlock' then
    local lang = b.classes[1]
    if lang and lang ~= 'text' then return nil end
    local n = code_lines(b)
    if n <= MAX_CODE then return math.ceil(n * 0.8) + 1 end
  elseif b.t == 'Table' then
    local n = table_rows(b)
    if n <= MAX_ROWS then return math.ceil(n * 0.95) + 2 end
  end
  return nil
end

local KEEP_INTRO = false -- keep an introducing paragraph with its block

local function intro_lines(b)
  if not KEEP_INTRO or b.t ~= 'Para' then return nil end
  local s = pandoc.utils.stringify(b)
  if not s:match(':%s*$') then return nil end
  return math.ceil(#s / LINE_CHARS) + 1
end

local function needspace(lines)
  return pandoc.RawBlock('latex',
    string.format('\\needspace{%d\\baselineskip}', lines))
end

-- a short paragraph between a heading and its block
local function short_para(b)
  if b.t ~= 'Para' then return nil end
  local n = math.ceil(#pandoc.utils.stringify(b) / LINE_CHARS)
  if n <= 4 then return n + 1 end
  return nil
end

function Blocks(blocks)
  local out = pandoc.List()
  for _, b in ipairs(blocks) do
    local n = need(b)
    if n then
      -- what moves with the block: a heading directly above it, or a
      -- heading and one short paragraph, so that a heading is never
      -- left above an empty half page; otherwise, with KEEP_INTRO, an
      -- introducing paragraph
      local moved = pandoc.List()
      local last = out[#out]
      local before = out[#out - 1]
      if last and last.t == 'Header' then
        moved:insert(out:remove(#out))
        n = n + 3
      elseif last and before and before.t == 'Header' and short_para(last) then
        n = n + 3 + short_para(last)
        local p = out:remove(#out)
        moved:insert(out:remove(#out))
        moved:insert(p)
      elseif last and intro_lines(last) then
        n = n + intro_lines(last)
        moved:insert(out:remove(#out))
      end
      out:insert(needspace(n))
      out:extend(moved)
    end
    out:insert(b)
  end
  return out
end
